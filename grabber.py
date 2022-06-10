#!/usr/bin/env python3


import argparse
import os
import sys

import cv2

from lib import DB
from lib import VideoCapture


def getArguments():
    '''Returns the arguments passed on the command line.'''
    parser = argparse.ArgumentParser(description="Grabs pictures of your face to be used in training of neural networks.")
    parser.add_argument("--videocapturedevice", type=int, required=False, default=0, help="The device ID")
    parser.add_argument("--infile", type=str, required=False, default=None, nargs="?", help="Input file (leave empty to use webcam.")
    parser.add_argument("--fps", type=float, required=False, default=30.0, help="The FPS the webcamera should use if device and not a file.")
    parser.add_argument("--label", type=str, required=True, help="The label you are going to take pictures for.")
    parser.add_argument("--basedir", type=str, required=False, default=os.path.dirname(os.path.abspath(__file__)),
        help="The base path to where the different data folders are found.")
    parser.add_argument("--dbfilename", type=str, required=False, default="", help="The database filename found under basedir.")
    return parser.parse_args()


if __name__ == "__main__":

    args = getArguments()
    db = DB(args.dbfilename)

    # We create label ID if it does not exist and get the label ID.
    labelId = db.getLabelId(args.label)
    if not labelId:
        labelId = db.addLabel(args.label)

    # We figure out the video source
    if args.infile:
        cap = VideoCapture(args.infile, args.fps)
    else:
        cap = VideoCapture(args.videocapturedevice, args.fps)

    for _, frame in cap:
        cv2.imshow("Grabber", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        if cv2.waitKey(1) & 0xFF == ord("s"):
            ret, encodedFrame = cv2.imencode('.jpg', frame)
            db.addFrame(encodedFrame.tobytes(), labelId)
