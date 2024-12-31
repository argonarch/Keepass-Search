from pykeepass import PyKeePass


class KeepassXC:
    def __init__(self, pathDB: str, pathPass: str):
        self.pathPass = pathPass
        self.pathDB = pathDB

        self.kp = PyKeePass(
            self.pathDB,
            keyfile=self.pathPass,
        )

    def search(self, query: str):
        entry = self.kp.find_entries(title=query, regex=True)
        print(entry)
        return entry

    def search_titles(self, query: str):
        entries = self.kp.find_entries(title=query, regex=True, first=False) or []
        listEntries = []
        for entry in entries:
            listEntries.append(entry.title)
        return listEntries

    def change_pathPass(self, new_path: str) -> None:
        """
        Change the path to the database file and lock the database.
        """
        self.pathPass = new_path

    def change_pathDB(self, new_path: str) -> None:
        """
        Change the path to the database file and lock the database.
        """
        self.pathDB = new_path


# hola = KeepassXC(
#     "/hdd/falcon/argonarch/Apps/KeepassXC/Passwords.kdbx",
#     "/hdd/falcon/argonarch/Apps/KeepassXC/pass",
# )
# print(hola.search_titles("Edesur"))
