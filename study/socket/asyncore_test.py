


# asyncore의 진입 함수 loop()
def loop (timeout=30.0, use_poll=0, map=None):
    if map is None:
        map=socket_map
    
    if use_poll:
        if hasattr (select, 'poll'): # 파이썬 2.0 이후 select 모듈에서 poll 정의
            poll_fun = poll3
        else:
            poll_fun = poll2
    else:
        poll_fun = poll
    while map:
        poll_fun (timeout, map)


def poll (timeout=0.0, map=None):
    if map is None:
        map = socket_map
    if map:
        r = []; w = []; e = []
        for fd, obj in map.items(): #1 
            if obj.readable():
                r.append (fd)
            if obj.writable():
                w.append (fd)
        r,w,e = select.select (r,w,e, timeout) #2

        for fd in r: #3
            try:
                obj = map[fd]
                try:
                    obj.handle_read_event()
            except ExitNow:
                raise ExitNow
            except:
                obj.handle_error()
        except KeyError:
            pass
    for fd in w: #4 
        try:
            obj = map[fd]
            try:
                obj.handle_write_event()
        except ExitNow:
            raise ExitNow
        except:
            obj.handle_error()
        except KeyError:
            pass

class dispatcher:
    debug = 0
    connected = 0
    accepting = 0 # 서버로 동작할 때 listen() 메쏘드가 1로 설정
    closing = 0
    addr = None
    def __init__ (self, sock=None, map=None):
        if sock:
            self.set_socket (sock, map)
            # I think it should inherit this anyway
            self.socket.setblocking (0) # 논블록킹(non-blocking) I/O
            self.connected = 1
        def add_channel (self, map=None):
            if map is None:
                map=socket_map
            map [self._fileno] = self

        def del_channel (self, map=None):
            fd = self._fileno
            if map is None:
                map=socket_map
            if map.has_key (fd):
                del map [fd]

        def create_socket (self, family, type):
            self.family_and_type = family, type
            self.socket = socket.socket (family, type)
            self.socket.setblocking(0)
            self._fileno = self.socket.fileno()
            self.add_channel()
        def set_socket (self, sock, map=None):
            self.__dict__[􀒔socket􀒔] = sock
            self._fileno = sock.fileno()
            self.add_channel (map)
        def set_reuse_addr (self):
        # 가능하다면 서버 포트를 재사용하려고 시도할 것.
            try:
                self.socket.setsockopt (
                    socket.SOL_SOCKET, socket.SO_REUSEADDR,
                    self.socket.getsockopt (socket.SOL_SOCKET,
                        socket.SO_REUSEADDR) | 1 )
            except:
                pass
        def readable (self):
            return 1
        def writable (self):
            return 1
