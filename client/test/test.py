#!/usr/bin/python3
import os 

def main():
	print (os.path.realpath(__file__), )
	print (__name__, )
	print (os.path.abspath(os.path.dirname(__file__)), )