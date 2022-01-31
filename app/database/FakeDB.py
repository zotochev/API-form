class FakeDB:
    forms = list()

    def get_form(self, form_id: int):
        if len(self.forms) > form_id:
            return self.forms[form_id]

    def insert(self, data: dict):
        self.forms.append(data)


db = FakeDB()

if __name__ == "__main__":
    db.insert({'foo1': 'bar1'})
    print(db.get_form(0))
