import { Component, OnDestroy, OnInit } from '@angular/core';
import { NbThemeService } from '@nebular/theme';
import { takeWhile } from 'rxjs/operators';

import { EventListService, Evento } from '../../../@core/data/event-list.service';

@Component({
  selector: 'ngx-event-list',
  styleUrls: ['./event-list.component.scss'],
  template: `
    <nb-card size="large">
      <nb-card-header>
        <span>Eventos</span>
        <div class="dropdown ghost-dropdown" ngbDropdown>
        </div>
      </nb-card-header>
      <nb-card-body>
        <ul class="event-list-list">
          <!--<li *ngFor="let item of eventList">-->
            <!--<div class="visited-date">-->
              <!--{{ item.date }}-->
            <!--</div>-->
            <!--<div class="evento-content">-->
              <!--<div class="title">Evento</div>-->
              <!--<div class="value">{{ item.content }} algo masdadsasd</div>-->
            <!--</div>-->
          <!--</li>-->
          <li *ngFor="let message of messages">
            <!--<div class="evento-content">-->
              <!--<nb-badge text="badgeText" status="warning" position="bottom left"></nb-badge>-->
                <!--<div class="title">Evento</div>-->
                <!--<div class="value">{{ message }} algo masdadsasd</div>-->
                <nb-card status="{{message.status}}">
                    <nb-card-header>{{message.content}}</nb-card-header>
                    <!--<nb-card-body>-->
                        <!--{{ message }}-->
                    <!--</nb-card-body>-->
                </nb-card>
            <!--</div>-->
          </li>
        </ul>
      </nb-card-body>
    </nb-card>
  `,
})
export class EventListComponent implements OnDestroy, OnInit {

  private alive = true;
  eventList: Evento[] = [];
  currentTheme: string;
  messages = [];
  connection;
  message;

  constructor(private themeService: NbThemeService,
              private eventService: EventListService) {
    this.themeService.getJsTheme()
      .pipe(takeWhile(() => this.alive))
      .subscribe(theme => {
        this.currentTheme = theme.name;
      });
  }

  sendMessage() {
    this.eventService.sendMessage(this.message);
    this.message = '';
  }

  ngOnInit() {
    this.connection = this.eventService.getMessages().subscribe(message => {
      this.messages = message;
    });

    this.getEventList();
  }

  getEventList() {
    this.eventService.getEventData()
      .subscribe(eventData => {
        this.eventList = eventData;
      });
  }

  ngOnDestroy() {
    this.alive = false;
    this.connection.unsubscribe();
  }
}
