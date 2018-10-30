import { Injectable } from '@angular/core';
import { of as observableOf,  Observable } from 'rxjs';
import * as socketIo from 'socket.io-client';

const SERVER_URL = 'http://10.1.0.5:5000';

export class Evento {
  date: string;
  content: string;
}

@Injectable()
export class EventListService {
  private getRandomString = Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 5);
  private socket;

  data = {};
  value = [
    'Mona',
    'Tue',
    'Wed',
    'Thu',
    'Fri',
    'Sat',
    'Sun',
  ];

  constructor() {
    this.data = {
      week: this.getDataWeek(),
    };
  }

  sendMessage(message) {
    this.socket.emit('add-message', message);
  }

  getMessages() {
    return new Observable<any>(observer => {
      this.socket = socketIo(SERVER_URL);
      this.socket.on('event', (data) => {
        observer.next(data);
      });
      return () => {
        this.socket.disconnect();
      };
    });

    // return observable;
  }

  private getDataWeek(): Evento[] {
    return this.value.map((week) => {
      return {
        date: week,
        content: this.getRandomString,
      };
    });
  }
  getEventData(): Observable<Evento[]> {
    return observableOf(this.data['week']);
  }
}
