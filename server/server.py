#! /usr/bin/python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import path
import rospkg
import subprocess
import sys

# Set up dictionary to hold rosrun nodes
nodes = dict()    
rp = rospkg.RosPack()

class MyHandler(BaseHTTPRequestHandler):            
    def do_GET(self):
        print "\nIncoming request!"
        try:
            if self.path.startswith("/PKG"):
                splitPath = self.path.split("/")
                if len(splitPath) > 2:
                    splitPath.remove('');
                    try:
                        pkg_path = rp.get_path(splitPath[1])
                    except rospkg.ResourceNotFound:
                        self.send_error(404, "Resource not found: %s" % splitPath[1])
                        return

                    subdir = self.path.replace('/PKG/' + splitPath[1], '')
                    filePath = pkg_path + subdir

                    try:
                        f = open(filePath) 
                    except:
                        self.send_error(404, 'Requested file not found: %s' % self.path)
                        return

                    self.send_response(200)
                    self.send_header('Content-Type', "type/html")
                    self.send_header('Content-Length', path.getsize(filePath))
                    self.end_headers()
                    self.wfile.write(f.read())
                    f.close()
                    return
                else:
                    self.send_error(404, 'Not enough information supplied: %s' % self.path)
            if self.path.startswith("/ROSRUN"):
                print "Received ROSRUN request!"
                splitPath = self.path.split("/")
                # splitPath = "","ROSRUN",NODEHANDLE,A,B,C,...N
                nodeHandle = splitPath[2]
                del splitPath[0:3]
                
                # If a node with this handle was already running, stop it
                if nodes.has_key(nodeHandle):
                    print "Already had a node with handle " + nodeHandle + ". Stopping old node and replacing it."
                    nodes[nodeHandle].kill()
                
                # Create a new node, include it in the list
                splitPath.insert(0,"rosrun")
                newProc = subprocess.Popen(splitPath, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)                
                nodes[nodeHandle] = newProc
                
                self.send_error(204)
                return
            if self.path.startswith("/ROSSTOP"):
                # Stop the specified node
                splitPath = self.path.split("/")
                nodeHandle = splitPath[2]
                if nodes.has_key(nodeHandle):
                    print "Stopping node " + nodeHandle
                    nodes[nodeHandle].kill()
                    
                self.send_error(204)    
                return
            return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

def main():
    # Begin TF throttle
    throttleTFProc = subprocess.Popen(["rosrun", "tf_throttle", "tf_throttle"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # Begin clock throttle
    #throttleClockProc = subprocess.Popen(["rosrun", "topic_tools", "throttle", "messages", "/clock", "1", "/clock_throttled"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        server = HTTPServer(('', 44644), MyHandler)
        print '\nStarted Rviz for Android resource server on port 44644'
        server.serve_forever()
    except KeyboardInterrupt:
        print 'Control-C received, shutting down server'
        throttleTFProc.kill()
        #throttleClockProc.kill()

        # Shut down all roslaunched processes
        for node in nodes:
            nodes[node].kill()
            
        server.socket.close()

if __name__ == '__main__':
    main()
