import { Injectable } from '@angular/core';
import { of as observableOf,  Observable } from 'rxjs';
import * as socketIo from 'socket.io-client';

const SERVER_URL = 'http://10.1.0.7:8070';
const socket = socketIo(SERVER_URL);

@Injectable()
export class EventListService {
  constructor() {}

  sendMessage(message) {
    socket.emit('enable_camera', message);
  }

  getMessages() {
    return new Observable<any>(observer => {
      socket.on('event', (data) => {
        observer.next(data);
      });
      return () => {
        socket.disconnect();
      };
    });
  }

  getCameras() {
      return new Observable<any>(observer => {
          socket.on('camera', (data) => {
              observer.next(data);
          });
          return () => {
              socket.disconnect();
          };
      });
    }
}
