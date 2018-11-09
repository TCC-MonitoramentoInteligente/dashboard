import {Component, OnDestroy, OnInit} from '@angular/core';

import { EventListService } from '../../../@core/data/event-list.service';

@Component({
  selector: 'ngx-security-cameras',
  styleUrls: ['./security-cameras.component.scss'],
  templateUrl: './security-cameras.component.html',
})

export class SecurityCamerasComponent implements OnDestroy, OnInit {
  cameraList;
  connection;
  selectedCamera;
  isSingleView = false;

    constructor(private eventService: EventListService) {}

    ngOnInit() {
        this.connection = this.eventService.getCameras().subscribe(message => {
            this.cameraList = message;
        });
    }
    sendMessage(message) {
        this.eventService.sendMessage(message);
    }

    ngOnDestroy() {
        this.connection.unsubscribe();
        }

  selectCamera(camera: any) {
    this.selectedCamera = camera;
    this.isSingleView = true;
    this.sendMessage(camera.id);
  }
}
