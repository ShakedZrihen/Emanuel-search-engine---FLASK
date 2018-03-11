from collections import OrderedDict
import os


config = {
    'user': 'root',
    'password': 'Shaked1234',
    'host': '127.0.0.1',
    'database': 'emanueldb',
    'raise_on_warnings': True,
}

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

TABLES = OrderedDict()

TABLES['documents'] = (
    "CREATE TABLE IF NOT EXISTS  `documents` ("
    "  `doc_id` int NOT NULL AUTO_INCREMENT,"
    "  `title` TEXT,"
    "  `author` TEXT,"
    "  `subject` TEXT,"
    "  `brief` TEXT,"
    "  `location` TEXT NOT NULL ,"
    "  PRIMARY KEY (`doc_id`)"
    ") ENGINE=InnoDB DEFAULT CHARACTER SET utf8"
)

TABLES['posting_file'] = (
    "CREATE TABLE IF NOT EXISTS `posting_file` ("
    "  `term` VARCHAR(255) NOT NULL,"
    "  `doc_id` INT NOT NULL,"
    "  `hits` INT NOT NULL,"
    "  PRIMARY KEY (`term`, `doc_id`),"
    "  CONSTRAINT `docTerm_ibfk_1` FOREIGN KEY (`doc_id`) "
    "  REFERENCES `documents` (`doc_id`) ON DELETE CASCADE ON UPDATE CASCADE"
    ") ENGINE=InnoDB DEFAULT CHARACTER SET utf8"
)




