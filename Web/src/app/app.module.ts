import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { AppComponent } from './app.component';
import { MainComponent } from './main/main.component';
import { GenerateComponent } from './generate/generate.component';

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
    GenerateComponent
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(appRoutes)
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
