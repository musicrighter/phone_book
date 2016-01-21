import sys
import os

class ArgumentError(Exception): pass

def create_phonebook(args):
	if args:
        phonebook_name = args.pop(0)
        create_phonebook(phonebook_name)
    else:
        raise ArgumentError("Not enough arguments!")

    filename = '%s.txt' % phonebook_name
    if os.path.exists(filename):
        print "That phonebook already exists!"
        quit()
    with open(filename, 'w') as f:
        pass

def add_entry(args):
    with open(filename, 'a') as f:
        f.write('%s\t%s' % (name, number))
        f.write('\n')   # add newline

def update(args):
   pass

def lookup(args):
    filename = '%s.txt' % phonebook_name
    with open(filename, 'r') as f:
        for line in f:
            entry_name, entry_number = line.strip().split('\t')
            if entry_name == name:
                print entry_name, entry_number

def delete(args):
    pass          

def main(argv):  
    if not argv:
        print "Not enough arguments"
        quit()
    command = argv.pop(0)   # the next arg will be the main command

    command_funcs = {
	    'create' : create,  # create is a function defined elsewhere
	    'add' : add,
	    'update' : update,
	    'delete' : delete,
	    'lookup' : lookup
	}

	func = command_funcs[command]
	func(argv)


if __name__ == '__main__':
    main(sys.argv[1:])