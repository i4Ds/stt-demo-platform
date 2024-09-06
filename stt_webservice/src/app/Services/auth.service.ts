import {Injectable} from '@angular/core';
import * as bcrypt from 'bcryptjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor() {

  }

  public login(password: string): Promise<boolean> {

    return new Promise<boolean>((resolve, reject) => {
      bcrypt.compare(password, "$2a$10$.nCU5iUlxKoSmkRXXH1Douxts2kstrah9nI9Qt7BEY/JA1pwYqPA.", function (err, result) {
        resolve(result)
      });
    });
  }
}
