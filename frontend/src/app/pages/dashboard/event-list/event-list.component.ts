import { Component, OnDestroy, OnInit } from '@angular/core';
import { NbThemeService } from '@nebular/theme';
import { takeWhile } from 'rxjs/operators';

import { EventListService } from '../../../@core/data/event-list.service';

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
          <li *ngFor="let message of messages">
            <nb-card status="{{message.status}}">
                <nb-card-header>{{message.content}}</nb-card-header>
            </nb-card>
          </li>
        </ul>
      </nb-card-body>
    </nb-card>
  `,
})
export class EventListComponent implements OnDestroy, OnInit {

  private alive = true;
  currentTheme: string;
  messages = [];
  connection;

  constructor(private themeService: NbThemeService,
              private eventService: EventListService) {
    this.themeService.getJsTheme()
      .pipe(takeWhile(() => this.alive))
      .subscribe(theme => {
        this.currentTheme = theme.name;
      });
  }

  ngOnInit() {
    this.connection = this.eventService.getMessages().subscribe(message => {
    this.messages = message;
    });
  }
  ngOnDestroy() {
    this.alive = false;
    this.connection.unsubscribe();
  }
}
