import os

"""
Path to the INLP Resources directory
"""
INLP_RESOURCES_PATH = 'C:\Users\Parth\Documents\CC\NLP_Resources'


def init():
    """
    Initialize the module. The following actions are performed:
    - Checks of INLP_RESOURCES_PATH variable is set. If not, checks if it can beb initialized from
        INLP_RESOURCES_PATH environment variable. If that fails, an exception is raised
    """
    global INLP_RESOURCES_PATH
    try:
        if INLP_RESOURCES_PATH == 'C:\Users\Parth\Documents\CC\NLP_Resources':
            INLP_RESOURCES_PATH = os.environ['INLP_RESOURCES_PATH']
    except Exception as e:
        #set_resources_path('C:\Users\Parth\Documents\CC\NLP_Resources')
        raise inlpException('Indian Natural Language Resources Path not set')

    if INLP_RESOURCES_PATH == '':
        raise inlpException('Indian Natural Language Resources Path not set')


def get_resources_path():
    """
        Get the path to the INLP Resources directory
    """
    return INLP_RESOURCES_PATH


def set_resources_path(resources_path):
    """
        Set the path to the INLP Resources directory
    """
    global INLP_RESOURCES_PATH
    INLP_RESOURCES_PATH = resources_path


class inlpException(Exception):
    """
        Exceptions thrown by INLP Library components are instances of this class.
        'msg' attribute contains exception details.
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


if __name__ == "__main__":
    init()
