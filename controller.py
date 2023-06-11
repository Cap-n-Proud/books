# Docker
# screen python3 /mnt/Software/200-Apps/imageflow/controller.py -iw "/mnt/Photos/000-InstantUpload/" -id "/mnt/Photos/005-PhotoBook/" -l "/mnt/Apps_Config/imageflow/" -s "/mnt/No_Share/secrets/imageflow/" -fc "/mnt/Apps_Config/imageflow/faceClassifier.pkl"

# Test
# python3 /mnt/Software/200-Apps/imageflow/controller.py -iw "/mnt/Photos/001-Process/IN/" -id "/mnt/Photos/001-Process/OUT/" -l "/mnt/Apps_Config/imageflow/" -s "/mnt/No_Share/secrets/imageflow/" -fc "/mnt/Apps_Config/imageflow/faceClassifier.pkl"


# ERRORS: video process colors are not cpatured correctley, GS reverse GEO does not work

import asyncio
import os
import datetime
from asyncio import Queue
from pathlib import Path
from datetime import datetime
import json

import logging
import sys
import argparse

# Importing the script to parse all the arguemnts
import parser

import ProcessMedia
import StopTimer

from config import fm_config


def init(args):

    logger = logging.getLogger()
    logger.setLevel(eval("logging." + args.logLevel))

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(eval("logging." + args.logLevel))

    FORMAT = "[%(asctime)s][%(name)s][%(levelname)s][%(message)s]"
    formatter = logging.Formatter(FORMAT)
    stdout_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(args.logFilePath + args.logName)
    file_handler.setLevel(eval("logging." + args.logLevel))
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)


def add_to_list_if_not_exist(lst, items):
    items = items.replace("[", "").replace("]", "").replace("'", "")
    items = items.strip().split(", ")
    for item in items:
        # print("item", item)
        if item not in lst:
            lst.append(item)
    return lst


# function that processes files in the imagesQueue
async def process_media(imagesQueue, processMedia, logger, args):
    stop_timer = StopTimer.StopTimer()
    while True:
        file = await imagesQueue.get()
        file_path = str(Path(args.imagesWatchDirectory) / file)

        await asyncio.sleep(args.watchDelay)
        logger.info(f"|Workflow| Processing: {str(file_path)}")

        stop_timer.reset()
        stop_timer.start()

        caption = ""
        faces = []
        ocr = ""
        objects = []
        colors = []
        reverseGeo = []
        imageTags = []
        KW = []
        transcription = ""

        # BOOK WORKFLOW
        # TO DO: remove file tagging from each function adn add a separate one like in the video workflow
        if file.lower().endswith(args.imageExtensions):
            if args.moveFileImage:
                file_path = await processMedia.move_file(file_path, args.imageDestinationDir)
            if args.tagImage:
                try:
                    imageTags = await processMedia.tag_image(file_path)
                except Exception as e:
                    logger.error(f"|tag_image| Error: {e}")
            if args.reverseGeotag:
                try:
                    reverseGeo = await processMedia.reverse_geotag(file_path)
                except Exception as e:
                    logger.error(f"|reverse_geotag| Error: {e}")
            if args.captionImage:
                try:
                    # Caption image
                    caption = str(await processMedia.caption_image(file_path))
                except Exception as e:
                    logger.error(f"|caption_image| Error: {e}")
            if args.classifyFaces:
                try:
                    # Identify faces
                    f = await processMedia.classify_faces(file_path)
                    if len(f):
                        faces = f
                except Exception as e:
                    logger.error(f"|classifyFacesImage| Error: {e}")

            if args.ocrImage:
                try:
                    # OCR texts in scene
                    ocr = str(
                        await processMedia.ocr_image(file_path, returnTag=False)
                    )
                except Exception as e:
                    logger.error(f"|ocrImage| Error: {e}")

            if args.idObjImage:
                try:
                    # Identfy objects
                    objects = await processMedia.id_obj_image(
                        file_path, returnTag=False
                    )
                except Exception as e:
                    logger.error(f"|idObjImage| Error: {e}")

            if args.getColorsImage:
                try:
                    colors = await processMedia.get_top_colors(file_path, n=5)

                except Exception as e:
                    logger.error(f"|getColorsImage| Error: {e}")
            if args.writeTagToImage:
                if reverseGeo is not None:
                    KW += reverseGeo
                if imageTags is not None:
                    KW += imageTags
                if objects is not None:
                    KW += objects
                if colors is not None:
                    KW += colors
                if faces is not None:
                    KW += faces
                noOCR = "None"
                if ocr == noOCR:
                    ocr = ""

                await processMedia.write_keywords_metadata_to_image_file(
                    file_path, keywords=KW, caption=str(caption), subject=ocr
                )
                if fm_config.COPY_TAGS_TO_IPTC == True:
                    await processMedia.copy_tags_to_IPTC(file_path)

        logger.info(f"Transcription: {transcription}|")
        logger.info(f"Caption: {caption}")
        logger.info(f"Keywords: {imageTags}")
        logger.info(f"Reverse Geo: {reverseGeo}")
        logger.info(f"Faces: {faces}")
        logger.info(f"OCR: {ocr}")
        logger.info(f"Objects: {objects}")
        logger.info(f"Colors: {colors}|")

        imagesQueue.task_done()
        stop_timer.stop()
        logger.info(
            "Media processed in: " +
            str(stop_timer.duration()) + " " + str(file_path)
        )


async def recursive_listdir(path, recursive=True):
    if not recursive:
        return os.listdir(path)
    else:
        result = []
        for root, dirs, files in os.walk(path):
            for name in files:
                result.append(os.path.join(root, name))
        return result


# function that watches a folder for new files
async def watch_folder(imagesQueue, args):
    processed_files = set()

    while True:
        # for file in os.listdir(args.imagesWatchDirectory):
        for file in await recursive_listdir(
            args.imagesWatchDirectory, recursive=args.watchRecursively
        ):
            if (
                file.lower().endswith(args.imageExtensions)
                or file.lower().endswith(args.videoExtensions)
            ) and file not in processed_files:
                imagesQueue.put_nowait(file)
                processed_files.add(file)
                # logger.debug("Added to queue:" + str(file))

        await asyncio.sleep(1)


async def main():
    imagesQueue = Queue()

    args, remaining_args = parser.parser.parse_known_args()
    # sys.path.append(args.configFileDirectory)
    # from config import fm_config

    FORMAT = "[%(asctime)s][%(name)s][%(levelname)s][%(message)s]"

    logger = logging.getLogger()
    logger.setLevel(eval("logging." + args.logLevel))
    formatter = logging.Formatter(FORMAT)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(eval("logging." + args.logLevel))
    stdout_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(args.logFilePath + args.logName)
    file_handler.setLevel(eval("logging." + args.logLevel))
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)

    ProcessMedia.logger = logger
    processMedia = ProcessMedia.ProcessMedia(args)
    logger.info("Server successfully started:" + str(datetime.now()))
    logger.info("Settings:" + str(vars(args)))
    # processMedia.create_ramdisk(fm_config.RAMDISK_DIR, fm_config.RAMDISK_SIZE_MB)

    # start the task that watches the folder for new files
    task1 = asyncio.create_task(watch_folder(imagesQueue, args))
    # start multiple tasks that process files in the imagesQueue
    task2 = [
        asyncio.create_task(process_media(
            imagesQueue, processMedia, logger, args))
        for _ in range(5)
    ]

    await asyncio.gather(task1, *task2)


if __name__ == "__main__":
    asyncio.run(main())
