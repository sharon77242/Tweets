import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';

@Injectable({
  providedIn: 'root'
})
export class TweetsService {

  constructor(private httpService: Http) { }

  GetStateTweetsTimes(stateName: string, successCallback: (timesList: Array<string>) => void): void {
    this.httpService.get('http://127.0.0.1:5000/' + stateName).subscribe((res: Response) => {
      successCallback(JSON.parse(res.text()));
    });
  }

  GetTweet(stateName: string, time: string, successCallback: (generatedResult: string) => void): void {
    this.httpService.post('http://127.0.0.1:5000/', {
      country: stateName,
      time: time
    }).subscribe((res: Response) => {
      successCallback(res.text());
    });
  }
}
