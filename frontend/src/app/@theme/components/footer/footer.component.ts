import { Component } from '@angular/core';

@Component({
  selector: 'ngx-footer',
  styleUrls: ['./footer.component.scss'],
  template: `
    <span class="created-by">Theme based on <b><a href="https://akveo.github.io/nebular" target="_blank">Nebular</a></b></span>
    <div class="socials">
      <a href="https://github.com/TCC-MonitoramentoInteligente" target="_blank" class="ion ion-social-github"></a>
    </div>
  `,
})
export class FooterComponent {
}
