#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' This is a demo template for using lief
    We've provide a simple example of loading binary file using lief
    As well as some help functions for binary file bytes modifying.
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

    # Load binary file using lief
    print "Loading the binary file 'cb'......"
    bin = lief.parse(in_binary)

    # Get the arch type
    bin_arch = bin.header.machine_type
    print "The file arch is : {}".format(str(bin_arch))
    if bin_arch != lief.ELF.ARCH.x86_64:
        print "Warning!: This is not a x86-64 file! the format is : {}".format(str(bin_arch))


if __name__ == "__main__":
    main()