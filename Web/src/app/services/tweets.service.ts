import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';

@Injectable({
  providedIn: 'root'
})
export class TweetsService {
  private static statesList: Array<{ label: string, value: string }>;
  private readonly SERVER_URL = 'http://127.0.0.1:5000/';

  constructor(private httpService: Http) { }

  GetStatesList(): Array<{ label: string, value: string }> {
    TweetsService.statesList = [
      { label: 'New York (NY)', value: 'NewYork' },
      { label: 'California (CA)', value: 'California' },
      { label: 'Los Angeles (LA)', value: 'LosAngeles' }
    ];

    return TweetsService.statesList;
  }

  GetStateTweetsTimes(
    stateName: string,
    successCallback: (timesList: Array<string>) => void,
    errorCallback?: () => void
  ): void {
    this.httpService.get(this.SERVER_URL + stateName).subscribe((res: Response) => {
      const result = JSON.parse(res.text());

      if (!(result[0] + '').includes('error')) {
        successCallback(result);
      } else {
        if (errorCallback) {
          errorCallback();
        }
      }
    });
  }

  GetTweet(stateName: string, time: string, successCallback: (generatedResult: string) => void): void {
    this.httpService.post(this.SERVER_URL, {
      country: stateName,
      time: time
    }).subscribe((res: Response) => {
      successCallback(res.text());
    });
  }
}
