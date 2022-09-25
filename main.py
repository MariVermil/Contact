class Contact:
    contact_id = -1
    surname = ''
    name = ''
    patronymic = ''
    phone_number = ''
    email_address = ''

    def parse_string(self, s):
        if s == '':
            return

        parts = s.split(',')
        name_parts = parts[0].split(' ')

        self.surname = name_parts[0]
        if len(name_parts) > 1:
            self.name = name_parts[1]
        if len(name_parts) > 2:
            self.patronymic = name_parts[2]

        self.phone_number = parts[1].strip()
        if not check_phone_number(self.phone_number):
            raise ValueError('Wrong phone number format')
        self.email_address = parts[2].strip()
        if not check_email_address(self.email_address):
            raise ValueError('Wrong email address format')

    def __init__(self, s, cur_id):
        self.parse_string(s)
        self.contact_id = cur_id

    def get_name(self):
        return ' '.join(filter(None, [self.surname, self.name, self.patronymic]))

    def get_string(self):
        res_string = self.get_name() + ','
        if self.phone_number != '':
            res_string += ' ' + self.phone_number
        res_string += ','
        if self.email_address != '':
            res_string += ' ' + self.email_address
        return res_string


def from_file(cur_contacts, filename):
    cur_contacts.clear()
    with open(filename, 'r') as file:
        cur_contacts.clear()
        line_num = 0
        for line in file:
            cur_contacts.append(Contact(line.rstrip(), line_num))
            line_num += 1


def to_file(cur_contacts, filename):
    with open(filename, 'w') as file:
        for to_write in cur_contacts:
            file.write(to_write.get_string() + '\n')


def print_contacts(cur_contacts):
    print('Results:\n')
    for to_print in cur_contacts:
        print('ID:', to_print.contact_id)
        print('Name:', to_print.get_name())
        if to_print.phone_number != '':
            print('Phone number:', to_print.phone_number)
        if to_print.email_address != '':
            print('Email address:', to_print.email_address)
        print()


def check_phone_number(phone_number):
    if phone_number == '':
        return True
    try:
        if phone_number[0] == '+' and 9 <= len(phone_number) - 1 <= 11:
            int(phone_number[1:])
            return True
        else:
            return False
    except ValueError:
        return False


def check_email_address(email_address):
    if email_address == '':
        return True
    parts = email_address.split('@')
    if len(parts) != 2 or parts[0] == '':
        return False
    parts2 = parts[1].split('.')
    if len(parts2) != 2 or '' in parts2:
        return False
    return True


contacts = []

while True:
    command = ' '.join(filter(None, input().split(' '))).split(' ')
    if command[0] == 'exit':
        break

    if command[0] == 'load':
        if len(command) == 2:
            try:
                from_file(contacts, command[1])
                print('Contacts have been loaded from', command[1])
            except FileNotFoundError:
                print('File not found.')

    if command[0] == 'save':
        if len(command) == 2:
            to_file(contacts, command[1])
            print('Contacts have been saved to', command[1])

    if command[0] == 'search':
        res = []
        if len(command) == 3 and command[1] in ['phone', 'email']:
            for contact in contacts:
                if command[1] == 'phone' and contact.phone_number == command[2] or \
                        command[1] == 'email' and contact.email_address == command[2]:
                    res.append(contact)

        if len(command) == 2 and command[1] in ['no_phone', 'no_email', 'no_phone_email']:
            for contact in contacts:
                if command[1] == 'no_phone' and contact.phone_number == '' or \
                        command[1] == 'no_email' and contact.email_address == '' or \
                        command[1] == 'no_phone_email' and contact.phone_number == '' and contact.email_address == '':
                    res.append(contact)

        if 3 <= len(command) <= 5 and command[1] == 'name':
            name = ' '.join(command[2:])
            for contact in contacts:
                temp = contact.get_name()
                if contact.get_name() == name:
                    res.append(contact)

        print_contacts(contacts)

    if command[0] == 'list' and len(command) == 1:
        print_contacts(contacts)

    if command[0] == 'edit' and len(command) == 4:
        contact_id = -1
        try:
            if command[1] in ['surname', 'name', 'patronymic', 'email', 'phone']:
                contact_id = int(command[2])
                found = False
                error = ''

                for contact in contacts:
                    if contact.contact_id == contact_id:
                        found = True
                        if command[1] == 'surname':
                            contact.surname = command[3]
                        elif command[1] == 'name':
                            contact.name = command[3]
                        elif command[1] == 'patronymic':
                            if contact.name != '':
                                contact.patronymic = command[3]
                            else:
                                error = 'name of ID ' + str(contact_id), ' is not set.'
                        elif command[1] == 'phone':
                            if not check_phone_number(command[3]):
                                error = 'wrong phone number format'
                            else:
                                contact.phone_number = command[3]
                        elif command[1] == 'email':
                            if not check_email_address(command[3]):
                                error = 'wrong email address format'
                            else:
                                contact.email_address = command[3]
                        break

                if error:
                    print('Error:', error)
                elif not found:
                    print('Could not find the contact with ID ', contact_id, '.', sep='')
                else:
                    print('Successfully changed ', command[1], ' to ', command[3], '.', sep='')

        except ValueError:
            print('Contact ID must be a number.')

    if command[0] == 'add' and 2 <= len(command) <= 5:
        try:
            contacts.append(Contact(' '.join(command[1:]), len(contacts)))
            print('Successfully added new contact.')
        except IndexError:
            print('Wrong contact format')
        except ValueError as e:
            print(str(e))

    if command[0] == 'remove' and len(command) == 2:
        try:
            contact_id = int(command[1])
            found = False
            for contact in contacts:
                if contact.contact_id == contact_id:
                    found = True
                    contacts.remove(contact)
                    break

            if not found:
                print('Could not find the contact with ID ', contact_id, '.', sep='')
            else:
                print('Successfully removed the contact with ID ', contact_id, '.', sep='')
        except ValueError:
            print('Contact ID must be a number.')

#                 ／＞　 フ
#                | 　_　_|  Мы с котиком устали это прогать, пожалуйста, будьте лояльным, мы старались(((
#               ／` ミ＿xノ  (а у одного из нас вообще лапки и он не прогал)
#              /　　　　 |
#             /　 ヽ　　 ﾉ
#            │　　|　|　|
#        ／￣|　　 |　|　|
#        | (￣ヽ＿_ヽ_)__)
#        ＼二)
