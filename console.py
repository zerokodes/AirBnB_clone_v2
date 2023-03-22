#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from shlex import split


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = "(hbnb) "

    __classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }

    def count(self, line):
        """count the number of instances of a class"""
        counter = 0
        try:
            my_list = split(line, " ")
            if my_list[0] not in self.__classes:
                raise NameError()
            objects = storage.all()
            for key in objects:
                name = key.split('.')
                if name[0] == my_list[0]:
                    counter += 1
            print(counter)
        except NameError:
            print("** class doesn't exist **")

    def strip_clean(self, args):
        """strips the argument and returns a string of command
        Args:
            args: input list of args
        Return:
            returns string of arguments
        """
        new_list = []
        new_list.append(args[0])
        try:
            my_dict = eval(
                    args[1][args[1].find('{').args[1].find('}')+1])
        except Exception:
            my_dict = None
        if isinstance(my_dict, dict):
            new_str = args[1][args[1].find('(')+1:args[1].find(')')]
            new_list.append(((new_str.split(", "))[0]).strip('"'))
            new_list.append(my_dict)
            return new_list
        new_str = args[1][args[1].find('(')+1:args[1].find(')')]
        new_list.append(" ".join(new_str.split(", ")))
        return " ".join(i for i in new_list)

    def default(self, line):
        """ retrieve all instance of a class and
            retrieve the number of instances
        """
        my_list = line.split('.')
        if len(my_list) >= 2:
            if my_list[1] == "all()":
                self.do_all(my_list[0])
            elif my_list[1] == "count()":
                self.count(my_list[0])
            elif my_list[1][:4] == "show":
                self.do_show(self.strip_clean(my_list))
            elif my_list[1][:7] == "destroy":
                self.do_destroy(self.strip_clean(my_list))
            elif my_list[1][:6] == "update":
                args = self.strip_clean(my_list)
                if isinstance(args, list):
                    obj = storage.all()
                    key = args[0] + ' ' + args[1]
                    for k, v in args[2].items():
                        self.do_update(key + ' "{}" "{}"'.format(k, v))
                else:
                    self.do_update(args)
        else:
            cmd.Cmd.default(self, line)

    def emptyline(self):
        """ Ignores empty spaces"""
        pass

    def do_quit(self, line):
        """ Quit command to exit the program"""
        return True

    def do_EOF(self, line):
        """ Quit command to exit program at EOF """
        return True

    def do_create(self, line):
        """ Create a new class with the given keys/values and print its id.
            Usage: create <class> <key>=<value> <key>=<value> ...
        """
        try:
            if not line:
                raise SyntaxError()
            my_list = line.split(" ")

            if my_list:
                cls_name = my_list[0]
            else:
                raise SyntaxError()
            kwargs = {}
            for pair in my_list[1:]:
                key, value = pair.split("=")
                if self.is_int(value):
                    kwargs[key] = int(value)
                elif self.is_float(value):
                    kwargs[key] = float(value)
                else:
                    value = value.replace('_', ' ')
                    kwargs[key] = value.strip('"\'')

            obj = self.__classes[cls_name](**kwargs)
            storage.new(obj)
            obj.save()
            print(obj.id)

        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, args):
        """ Prints string representation of an object
            Execeptions:
                SyntaxError: When no args are given
                NameError: When no object with name exists
                IndexError: When no id is given
                KeyError: When wrong id is given
        """
        try:
            if not args:
                raise SyntaxError()
            my_list = args.split(" ")
            if my_list[0] not in self.__classes:
                raise NameError()
            if len(my_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = my_list[0] + '.' + my_list[1]
            if key in objects:
                print(objects[key])
            else:
                raise KeyError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, args):
        """ Destroys a specified object
        Exceptions:
            NameError: when there is no object with the name
            SyntaxError: when there are no args given
            IndexError: when ther is no id given
            KeyError: when there is no valid id given
        """
        try:
            if not args:
                raise SyntaxError()
            my_list = args.split(" ")
            if my_list[0] not in self.__classes:
                raise NameError()
            if len(my_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = my_list[0] + '.' + my_list[1]
            if key in objects:
                del objects[key]
                storage.save()
            else:
                raise KeyError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def do_all(self, line):
        """ Shows all objects, or all objects of a class"""
        objects = storage.all()
        my_list = []
        if not line:
            for key in objects:
                my_list.append(objects[key])
            print(my_list)
            return
        try:
            args = line.split(" ")
            if args[0] not in self.__classes:
                raise NameError()
            for key in objects:
                name = key.split('.')
                if name[0] == args[0]:
                    my_list.append(objects[key])
            print(my_list)
        except NameError:
            print("** class doesn't exist **")

    def do_update(self, args):
        """ Updates a certain object with new info """
        c_name = c_id = att_name = att_val = kwargs = ''

        # isolate cls from id/args, ex: (<cls>, delim, <id/args>)
        args = args.partition(" ")
        if args[0]:
            c_name = args[0]
        else:  # class name not present
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.__classes:  # class name invalid
            print("** class doesn't exist **")
            return

        # isolate id from args
        args = args[2].partition(" ")
        if args[0]:
            c_id = args[0]
        else:  # id not present
            print("** instance id missing **")
            return

        # generate key from class and id
        key = c_name + "." + c_id

        # determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # first determine if kwargs or args
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []  # reformat kwargs into list, ex: [<name>, <value>, ...]
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:  # isolate args
            args = args[2]
            if args and args[0] == '\"':  # check for quoted arg
                second_quote = args.find('\"', 1)
                att_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')

            # if att_name was not quoted arg
            if not att_name and args[0] != ' ':
                att_name = args[0]
            # check for quoted val arg
            if args[2] and args[2][0] == '\"':
                att_val = args[2][1:args[2].find('\"', 1)]

            # if att_val was not quoted arg
            if not att_val and args[2]:
                att_val = args[2].partition(' ')[0]

            args = [att_name, att_val]

        # retrieve dictionary of current objects
        new_dict = storage.all()[key]

        # iterate through attr names and values
        for i, att_name in enumerate(args):
            # block only runs on even iterations
            if (i % 2 == 0):
                att_val = args[i + 1]  # following item is value
                if not att_name:  # check for att_name
                    print("** attribute name missing **")
                    return
                if not att_val:  # check for att_value
                    print("** value missing **")
                    return
                # type cast as necessary
                if att_name in HBNBCommand.types:
                    att_val = HBNBCommand.types[att_name](att_val)

                # update dictionary with name, value pair
                new_dict.__dict__.update({att_name: att_val})

        new_dict.save()  # save updates to file

    @staticmethod
    def is_int(n):
        """ checks if int"""
        try:
            int(n)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_float(n):
        try:
            float(n)
            return True
        except ValueError:
            return False


if __name__ == "__main__":
    HBNBCommand().cmdloop()
