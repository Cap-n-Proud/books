# Application configuration File
################################

# Directory To Watch, If not specified, the following value will be considered explicitly.
# DOCUMENTS_WATCH_DIRECTORY = "/home/paolo/Downloads/"
IMAGES_WATCH_DIRECTORY = "/mnt/Photos/000-InstantUpload/"

# Delay Between Watch Cycles In Seconds
WATCH_DELAY = 3

# TO BE IMPLEMENTED: TO BE ABLE TO RESUME FILES
# MIN_AGE = 300

# Check The WATCH_DIRECTORY and its children
WATCH_RECURSIVELY = True

# whether to watch for directory events
# DO_WATCH_DIRECTORIES = True

DOC_EXTENSIONS = (
    ".txt",
    ".trc",
    ".log",
    ".pdf",
    ".py",
    ".doc",
    ".docx",
    ".ppt",
    ".pptx",
    ".csv",
    ".dat",
    ".bat",
    ".sh",
    ".jar",
    ".htm",
    ".html",
    ".css",
    ".js",
)


# EXCEPTION_PATTERN = ["EXCEPTION", "FATAL", "ERROR"]

LOG_NAME = "books_dev.log"
LOG_FILEPATH = "/mnt/Apps_Config/books/"
LOG_LEVEL = "INFO"

SECRETS_PATH = "./secrets/"
# CONFIG_PATH = "/mnt/Software/200-Apps/imageflow/config/"
#SECRETS_PATH = "/app/imageflow/imageflow_secrets/"
#CONFIG_PATH = "/app/imageflow/config/"


# --------------------------- Workflow config ---------------------------

CAPTION_IMAGE = True
TAG_IMAGE = True
REVERSE_GEOTAG = True
CLASSIFY_FACES = True
OCR_IMAGE = True
COPY_TAGS_TO_IPTC = False
GET_COLORS_IMAGE = True
ID_OBJ = True
MOVE_FILE_IMAGE = False
WRITE_TAGS_TO_IMAGE = True
