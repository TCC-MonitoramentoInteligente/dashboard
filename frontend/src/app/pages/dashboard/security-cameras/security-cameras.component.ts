import { Component } from '@angular/core';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable()
export class ConfigService {
    constructor(private http: HttpClient) { }
    get_video() {
        return this.http.get('http://0.0.0.0:5000/video-debug');
    }
}

@Component({
  selector: 'ngx-security-cameras',
  styleUrls: ['./security-cameras.component.scss'],
  templateUrl: './security-cameras.component.html',
})
export class SecurityCamerasComponent {
  config: ConfigService;
  cameras: any[] = [{
    title: 'Camera #1',
    // source: 'assets/images/camera1.jpg',
    //   source: this.config.get_video(),
      source: 'http://0.0.0.0:5000/video-debug',
  }, {
    title: 'Camera #2',
    source: 'assets/images/camera2.jpg',
  }, {
    title: 'Camera #3',
    source: 'assets/images/camera3.jpg',
  }, {
    title: 'Camera #4',
    source: 'assets/images/camera4.jpg',
  }];

  selectedCamera: any = this.cameras[0];
  isSingleView = false;

  selectCamera(camera: any) {
    this.selectedCamera = camera;
    this.isSingleView = true;
  }
}
