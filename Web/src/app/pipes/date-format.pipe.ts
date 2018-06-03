import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'dateFormat',
  pure: true
})
export class DateFormatPipe implements PipeTransform {

  transform(date: string): string {
    const numbers: Array<string> = date.split('_');
    const result = numbers[0] + '/' + numbers[1] + '/' + numbers[2] + ' ' + numbers[3] + ':' + numbers[4] + ':' + numbers[5];

    return result;
  }

}
