import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HttpModule } from '@angular/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { MainComponent } from './main/main.component';
import { GenerateComponent } from './generate/generate.component';
import { LiveMapComponent } from './live-map/live-map.component';

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
    LiveMapComponent
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(appRoutes),
    HttpModule,
    FormsModule,
    ReactiveFormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
