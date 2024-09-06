import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LongComponent } from './long.component';

describe('LongComponent', () => {
  let component: LongComponent;
  let fixture: ComponentFixture<LongComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LongComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(LongComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
