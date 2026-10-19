import { Component, OnInit } from '@angular/core';

import { CommonModule } from '@angular/common';

import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';

import { Router } from '@angular/router';

import { TripDataService } from '../services/trip-data';

import { User } from '../models/user';



@Component({

  selector: 'app-login',

  standalone: true,

  imports: [CommonModule, ReactiveFormsModule],

  templateUrl: './login.html',

  styleUrl: './login.css'

})

export class Login implements OnInit {

  loginForm!: FormGroup;

  submitted = false;



  constructor(

    private formBuilder: FormBuilder,

    private router: Router,

    private tripService: TripDataService

  ) {}



  ngOnInit(): void {

    this.loginForm = this.formBuilder.group({

      email: ['', [Validators.required, Validators.email]],

      password: ['', Validators.required]

    });

  }



  public onSubmit(): void {

  this.submitted = true;

  if (this.loginForm.valid) {

    const user: User = {
      name: '',
      email: this.loginForm.value.email
    };

    const password = this.loginForm.value.password;

    this.tripService.login(user, password)

      .subscribe({

        next: (data: any) => {

          localStorage.setItem('travlr-token', data.token);

          this.router.navigate(['']);

        },

        error: (error: any) => {

          console.log('Error: ' + error);

        }

      });

  }

}


  get f() {

    return this.loginForm.controls;

  }

}
