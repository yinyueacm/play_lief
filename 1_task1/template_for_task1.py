#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' This is a template for task 1
    Finish the modify_bin() function
'''

import lief

def memFetch(data, offset, nbytes):
    fdata = data[offset:offset+nbytes]
    return fdata


def memWrite(data, offset, nbytes, mem):
    data = data[:offset] + mem + data[offset+nbytes:]
    return data


def memAdd(data, offset, nbytes, mem):
    data = data[:offset] + mem + '\x00' * (nbytes - len(mem)) + data[offset:]
    #data = data + '\x00'
    return data


def memCopy(filename, offset, nbytes, mem):
    fd = open(filename,'rb')
    data = fd.read()
    fd.close()
    data = data[:offset] + mem + data[offset+nbytes:]
    fd = open(filename,'wb')
    fd.write(data)
    fd.close()


def main():
    in_binary = "cb"

    new_bin = modify_bin(in_binary)

    # Write to new file
    fname = in_binary + "_modified"
    out_fd = open(fname, 'wb')
    print "Write to file: {}".format(fname)
    out_fd.write(new_bin)
    out_fd.close()


# ***************************************************************************
# Start your work in modify_bin()

# You may need some imports or define here

# (...)

def modify_bin(in_bin):
    bin = lief.parse(in_bin)
    in_fd = open(in_bin, 'rb')
    out_data = in_fd.read()

    # finish the work
    # (...)

    return out_data

# ***************************************************************************


if __name__ == "__main__":
    main()