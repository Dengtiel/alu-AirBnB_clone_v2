#!/usr/bin/python3
""" Console Module """
import cmd
import sys
import shlex
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
    }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
        'number_rooms': int, 'number_bathrooms': int,
        'max_guest': int, 'price_by_night': int,
        'latitude': float, 'longitude': float
    }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)', end='')

    def precmd(self, line):
        """Reformat command line for advanced command syntax."""
        _cmd = _cls = _id = _args = ''

        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:
            pline = line[:]

            # isolate class name
            _cls = pline[:pline.find('.')]

            # isolate command
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # parse arguments
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args
                pline = pline.partition(', ')

                # isolate id
                _id = pline[0].replace('\"', '').replace("'", "")

                # if arguments exist
                pline = pline[2].strip()
                if pline:
                    if (pline[0] == '{' and pline[-1] == '}' and
                            isinstance(eval(pline), dict)):
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
            
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """Prints the help documentation for quit"""
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """Handles EOF to exit program"""
        print()
        exit()

    def help_EOF(self):
        """Prints the help documentation for EOF"""
        print("Exits the program without formatting\n")

    def emptyline(self):
        """Overrides the emptyline method of CMD"""
        pass

    def do_create(self, args):
        """Create an object of any class"""
        if not args:
            print("** class name missing **")
            return
        
        arg_list = args.split()
        if arg_list[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
            
        new_instance = HBNBCommand.classes[arg_list[0]]()
        for param in arg_list[1:]:
            if '=' in param:
                key, value = param.split('=', 1)
                if value[0] == value[-1] == '"':
                    value = value[1:-1].replace('_', ' ').replace('\\"', '"')
                elif '.' in value:
                    try:
                        value = float(value)
                    except ValueError:
                        continue
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        continue
                setattr(new_instance, key, value)
        
        new_instance.save()
        print(new_instance.id)

    def help_create(self):
        """Help information for the create method"""
        print("Creates a class of any type")
        print("[Usage]: create <className> [<param>=<value> ...]\n")

    def do_show(self, args):
        """Method to show an individual object"""
        args = args.split()
        if not args:
            print("** class name missing **")
            return
        
        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
            
        if len(args) < 2:
            print("** instance id missing **")
            return
            
        key = f"{args[0]}.{args[1]}"
        all_objs = storage.all()
        if key not in all_objs:
            print("** no instance found **")
            return
            
        print(all_objs[key])

    def help_show(self):
        """Help information for the show command"""
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """Destroys a specified object"""
        args = args.split()
        if not args:
            print("** class name missing **")
            return
            
        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
            
        if len(args) < 2:
            print("** instance id missing **")
            return
            
        key = f"{args[0]}.{args[1]}"
        all_objs = storage.all()
        if key not in all_objs:
            print("** no instance found **")
            return
            
        del all_objs[key]
        storage.save()

    def help_destroy(self):
        """Help information for the destroy command"""
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """Shows all objects, or all objects of a class"""
        obj_list = []
        all_objs = storage.all()
        
        if not args:
            for obj in all_objs.values():
                obj_list.append(str(obj))
        else:
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for key, obj in all_objs.items():
                if key.split('.')[0] == args:
                    obj_list.append(str(obj))
                    
        print(obj_list)

    def help_all(self):
        """Help information for the all command"""
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for key in storage.all():
            if args == key.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """Help information for count"""
        print("Usage: count <class_name>")

    def do_update(self, args):
        """Updates a certain object with new info"""
        args = shlex.split(args)
        if not args:
            print("** class name missing **")
            return
            
        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
            
        if len(args) < 2:
            print("** instance id missing **")
            return
            
        key = f"{args[0]}.{args[1]}"
        all_objs = storage.all()
        if key not in all_objs:
            print("** no instance found **")
            return
            
        if len(args) < 3:
            print("** attribute name missing **")
            return
            
        if len(args) < 4:
            print("** value missing **")
            return
            
        obj = all_objs[key]
        attr_name = args[2]
        attr_value = args[3]
        
        if attr_name in HBNBCommand.types:
            attr_value = HBNBCommand.types[attr_name](attr_value)
            
        setattr(obj, attr_name, attr_value)
        obj.save()

    def help_update(self):
        """Help information for the update class"""
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()