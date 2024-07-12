from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    booking_start = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    booking_end = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Booking
        fields = ['table', 'booking_start', 'booking_end']

    def clean(self):
        cleaned_data = super().clean()
        table = cleaned_data.get("table")
        booking_start = cleaned_data.get("booking_start")
        booking_end = cleaned_data.get("booking_end")

        if booking_start and booking_end:
            # Convert booking_start and booking_end to strings before comparison
            booking_start_str = booking_start.isoformat()
            booking_end_str = booking_end.isoformat()

            if booking_start_str >= booking_end_str:
                raise forms.ValidationError("The booking end time must be after the start time.")

            overlapping_bookings = Booking.objects.filter(
                table=table,
                booking_end__gt=booking_start,
                booking_start__lt=booking_end
            )
            if overlapping_bookings.exists():
                raise forms.ValidationError("This table is already booked for the selected time period.")

        return cleaned_data
