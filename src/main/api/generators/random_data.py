import random
from faker import Faker

faker = Faker()


class RandomData:
    @staticmethod
    def get_username() -> str:
        return ''.join(faker.random_letters(length=random.randint(3, 15)))

    @staticmethod
    def get_password() -> str:
        upper = [letter.upper() for letter in faker.random_letters(length=3)]
        lower = [letter.lower() for letter in faker.random_letters(length=3)]
        digits = [str(faker.random_digit()) for _ in range(3)]
        special = [random.choice('!@#$%^&')]
        password = upper + lower + digits + special
        random.shuffle(password)
        return ''.join(password)

    @staticmethod
    def get_profile_name() -> str:
        from faker import Faker
        faker = Faker()

        first = faker.first_name()
        last = faker.last_name()

        first = ''.join(filter(str.isalpha, first))
        last = ''.join(filter(str.isalpha, last))

        return f"{first} {last}"