import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class Auth {

  public isLoggedIn(): boolean {
    return localStorage.getItem('travlr-token') !== null;
  }

  public getToken(): string | null {
    return localStorage.getItem('travlr-token');
  }

  public logout(): void {
    localStorage.removeItem('travlr-token');
  }

}