import sys
import getopt
import concurrent.futures
# from multiprocessing.pool import ThreadPool
import subprocess

verbose = False


def start_server(index, detective, ghost):
    global verbose
    server = subprocess.Popen(["py", "./server.py", str(index)], shell=True, stdout=subprocess.PIPE)
    running = True
    clients = None
    while running:
        line = server.stdout.readline()
        if line != '':
            str_line = line.rstrip().decode("utf-8")
            if verbose:
                print(str_line)
            if str_line.startswith("PORT:"):
                port = str_line[5:]
                executor, clients = start_clients(port, detective, ghost)
            if str_line == "END SERVER":
                running = False
                server.communicate()
    for client in concurrent.futures.as_completed(clients):
        s = clients[client]
        try:
            data = client.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (s, exc))
        else:
            return data
    return 0


def start_client(index, port, detective, ghost):
    global verbose
    if index == 0:
        client = subprocess.Popen(["py", "./client.py", "-p", str(port), "-f", ghost, "-g", "True"],
                                  shell=True, stdout=subprocess.PIPE)
    else:
        client = subprocess.Popen(["py", "./client.py", "-p", str(port), "-f", detective, "-g", "False"],
                                  shell=True, stdout=subprocess.PIPE)
    running = True
    while running:
        line = client.stdout.readline()
        if line != "":
            str_line = line.rstrip().decode("utf-8")
            if str_line == "END":
                running = False
            elif verbose:
                print(str_line)
    return 0


def start_clients(port, detective, ghost):
    n_client = 2
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=n_client)
    clients = {executor.submit(start_client, i, port, detective, ghost): i for i in range(n_client)}
    return executor, clients


def parse_args(argv):
    global verbose
    my_opts, args = getopt.getopt(argv[1:], "d:g:n:v:")

    detective = ""
    ghost = ""
    num_game = 0
    for o, a in my_opts:
        if o == '-d':
            detective = a
        elif o == '-n':
            num_game = int(a)
        elif o == "-g":
            ghost = a
        elif o == "-v":
            verbose = a == "True"
        else:
            print("Usage: %s -n number_of_game -g ghost.py -d detective.py" % sys.argv[0])
    print("Detective file : %s and Ghost file: %s" % (detective, ghost))
    return num_game, detective, ghost


def main(argv):
    num_game, detective, ghost = parse_args(argv)
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_game) as executor:
        # Start the load operations and mark each future with its URL
        servers = {executor.submit(start_server, i, detective, ghost): i for i in range(num_game)}
        for server in concurrent.futures.as_completed(servers):
            s = servers[server]
            try:
                data = server.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (s, exc))
            else:
                print("end")
                return data


if __name__ == "__main__":
    main(sys.argv)
