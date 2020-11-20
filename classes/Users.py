from classes.storage import Loader, NamesStorage as ns


class Users:
    file_way = "files/users.txt"
    jsn_file_way = '../files/storage.json'

    @classmethod
    def authorize(cls, user_id, user_group):
        cls.delete_user_data(user_id)
        cls.__put_user_data_to_file(user_id, user_group)

    @classmethod
    def delete_user_data(cls, id_of_user_to_delete):
        file = Loader.load_data()
        try:
            del file[str(id_of_user_to_delete)]
            Loader.save_data(file)
        except:
            pass

    @classmethod
    def __put_user_data_to_file(cls, user_id, user_group):
        file = Loader.load_data()
        file[user_id] = {
                ns.user_group: user_group,
                ns.remind: True
            }
        Loader.save_data(file)

    @classmethod
    def get_info_by_user_id(cls, user_id):
        file = Loader.load_data()
        return file[str(user_id)]

    @classmethod
    def get_group_by_user_id(cls, user_id):
        return cls.get_info_by_user_id(user_id)[ns.user_group]

    @classmethod
    def get_remind_by_user_id(cls, user_id):
        return cls.get_info_by_user_id(user_id)[ns.remind]

    @classmethod
    def switch_on_remind_by_user_id(cls, user_id):
        file = Loader.load_data()
        file[str(user_id)][ns.remind] = True
        Loader.save_data(file)

    @classmethod
    def switch_off_remind_by_user_id(cls, user_id):
        file = Loader.load_data()
        file[str(user_id)][ns.remind] = False
        Loader.save_data(file)

    @classmethod
    def is_user_in_data_base(cls, user_id):
        file = Loader.load_data()
        if str(user_id) in file:
            return True
        else:
            return False


class LineTool:
    # line_example = "12345,21/1"

    @classmethod
    def get_user_id_from_line(cls, line):
        return int(line.split(',')[0])

    @classmethod
    def get_user_group_from_line(cls, line):
        return line.split(',')[1].rstrip()

    @classmethod
    def get_user_remainder_from_line(cls, line):
        return line.split(',')[2].rstrip()
