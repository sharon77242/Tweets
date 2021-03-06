import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HttpModule } from '@angular/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { MainComponent } from './main/main.component';
import { GenerateComponent } from './generate/generate.component';
import { LiveMapComponent } from './live-map/live-map.component';
import { DateFormatPipe } from './pipes/date-format.pipe';
import { AboutComponent } from './about/about.component';

const appRoutes: Routes = [
  // { path: 'hero/:id',      component: HeroDetailComponent },
  {
    path: 'Generate',
    component: GenerateComponent
  },
  {
    path: 'Main',
    component: MainComponent
  },
  {
    path: 'LiveMap',
    component: LiveMapComponent
  },
  {
    path: 'About',
    component: AboutComponent
  },
  {
    path: '',
    redirectTo: '/Main',
    pathMatch: 'full'
  },
  { path: '**', redirectTo: '/Main' }
];

@NgModule({
  declarations: [
    AppComponent,
    MainComponent,
    GenerateComponent,
    LiveMapComponent,
    DateFormatPipe,
    AboutComponent
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(appRoutes),
    HttpModule,
    FormsModule,
    ReactiveFormsModule
  ],
  providers: [
    DateFormatPipe
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
