import os


def fetch_api_key(file_name):
    """
    Fetch the API key from the key file, which is not supposed to be public
    :param file_name:
    :return:
    """
    if os.path.isfile(file_name):
        f = open(file_name)
        api_key = f.read()
        f.close()
        return api_key
    else:
        print "ERROR: Path file is missing."
        return None


def fetch_email_credentials(file_name):

    if os.path.isfile(file_name):
        f = open(file_name)
        [username, password] = f.read().split()
        f.close()
        return [username, password]
    else:
        print "ERROR: Credential file is missing."
        return None


if __name__ == "__main__":
    print fetch_email_credentials('credentials')

