import { Component, OnInit } from '@angular/core';

import { CommonModule } from '@angular/common';

import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';

import { ActivatedRoute, Router } from '@angular/router';

import { TripDataService } from '../services/trip-data';



@Component({

  selector: 'app-edit-trip',

  standalone: true,

  imports: [CommonModule, ReactiveFormsModule],

  templateUrl: './edit-trip.html',

  styleUrl: './edit-trip.css'

})

export class EditTrip implements OnInit {

  editForm!: FormGroup;

  submitted = false;

  tripCode = '';



  constructor(

    private formBuilder: FormBuilder,

    private router: Router,

    private route: ActivatedRoute,

    private tripService: TripDataService

  ) {}



  ngOnInit(): void {

  this.tripCode = this.route.snapshot.paramMap.get('tripCode') || '';

  this.editForm = this.formBuilder.group({

    _id: [],

    code: ['', Validators.required],

    name: ['', Validators.required],

    length: ['', Validators.required],

    start: ['', Validators.required],

    resort: ['', Validators.required],

    perPerson: ['', Validators.required],

    image: ['', Validators.required],

    description: ['', Validators.required]

  });

  this.tripService.getTrip(this.tripCode).subscribe({

    next: (data: any) => {

      const trip = Array.isArray(data) ? data[0] : data;

      if (trip) {

        this.editForm.patchValue({

          _id: trip._id,

          code: trip.code,

          name: trip.name,

          length: trip.length,

          start: trip.start ? trip.start.substring(0, 10) : '',

          resort: trip.resort,

          perPerson: trip.perPerson,

          image: trip.image,

          description: trip.description

        });

      }

    },

    error: (error: any) => {

      console.log('Error: ' + error);

    }

  });

}


  public onSubmit(): void {

    this.submitted = true;



    if (this.editForm.valid) {

      this.tripService.updateTrip(this.editForm.value)

        .subscribe({

          next: (data: any) => {

            console.log(data);

            this.router.navigate(['']);

          },

          error: (error: any) => {

            console.log('Error: ' + error);

          }

        });

    }

  }



  get f() {

    return this.editForm.controls;

  }

}