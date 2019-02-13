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

    new_bin = modify_bin(in_binary)

    # Write to new file
    fname = in_binary + "_modified"
    out_fd = open(fname, 'wb')
    print "Write to file: {}".format(fname)
    out_fd.write(new_bin)
    out_fd.close()


# ***************************************************************************
# Start your work in modify_bin()

from struct import *

p_filesz_off = 0x20
p_memsz_off = 0x28

def modify_bin(in_bin):
    bin = lief.parse(in_bin)
    in_fd = open(in_bin, 'rb')
    out_data = in_fd.read()

    # get 'note.ABI-tag' section
    if bin.has_section(".note.ABI-tag"):
        nat_sec = bin.get_section(".note.ABI-tag")
        nat_size = nat_sec.size

        new_seg_idx = -1
        cb_phoff = bin.header.program_header_offset
        cb_phentsize = bin.header.program_header_size
        for seg in bin.segments:
            new_seg_idx += 1
            if seg.type == lief.ELF.SEGMENT_TYPES.NOTE:
                print "Found the 'NOTE' segment"
                seg_offset = cb_phoff + cb_phentsize * new_seg_idx
                # changing file size
                w_off = seg_offset + p_filesz_off
                w_value = pack('l', nat_size)
                out_data = memWrite(out_data, w_off, 8, w_value)
                print hex(w_off), hex(nat_size)

                # changing mem size
                w_off = seg_offset + p_memsz_off
                w_value = pack('l', nat_size)
                out_data = memWrite(out_data, w_off, 8, w_value)
                print hex(w_off), hex(nat_size)



    else:
        print "There is no section with name '.note.ABI-tag'!"
        exit(1)


    return out_data

# ***************************************************************************


if __name__ == "__main__":
    main()