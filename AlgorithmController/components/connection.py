import paramiko
import tkinter.messagebox


# path to json file on Xavier
XAVIER_PATH = 'Xavier_AUV/configs/tasks.json'
# path to json file on this device
SELF_PATH = 'temp.json'


class Connection():

    def __init__(self):
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect_to_server(self, username, password) -> bool:
        """
        Connects to the server, return True if success
        :param username: user@host
        :param password: password
        :return:
        """
        success = False
        name, host = username.split('@')
        try:
            self.ssh_client.connect(hostname=host,
                                    username=name,
                                    password=password)
            success = True
        except:
            pass
        return success

    def load_json(self) -> None:
        """
        Loads json from Xavier
        :return:
        """
        try:
            ftp_client = self.ssh_client.open_sftp()
            ftp_client.get(XAVIER_PATH, SELF_PATH)
        except Exception as e:
            tkinter.messagebox.showinfo('Error', e)
        finally:
            ftp_client.close()

    def send_json(self) -> None:
        """
        Send json to Xavier
        :return:
        """
        try:
            ftp_client = self.ssh_client.open_sftp()
            ftp_client.put(SELF_PATH, XAVIER_PATH)
        except Exception as e:
            tkinter.messagebox.showinfo('Error', e)
        finally:
            ftp_client.close()
