import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  menuItems = [
    { title: 'Home', url: '/Main' },
    { title: 'Generate', url: '/Generate' },
    { title: 'Live Map', url: '/LiveMap' },
    { title: 'About', url: '#' }
  ]
}
