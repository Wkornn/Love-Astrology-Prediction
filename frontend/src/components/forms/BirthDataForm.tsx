import { useState } from 'react';
import type { ChangeEvent } from 'react';
import { LocationSearch } from './LocationSearch';

export type BirthData = {
  date: string;
  time: string;
  latitude: string;
  longitude: string;
}

interface BirthDataFormProps {
  data: BirthData;
  onChange: (data: BirthData) => void;
  label?: string;
  errors?: Partial<Record<keyof BirthData, string>>;
}

export const BirthDataForm = ({ data, onChange, label, errors = {} }: BirthDataFormProps) => {
  const [unknownTime, setUnknownTime] = useState(false);

  const handleChange = (field: keyof BirthData) => (e: ChangeEvent<HTMLInputElement>) => {
    onChange({ ...data, [field]: e.target.value });
  };

  const handleUnknownTimeChange = (e: ChangeEvent<HTMLInputElement>) => {
    const checked = e.target.checked;
    setUnknownTime(checked);
    if (checked) {
      onChange({ ...data, time: '12:00' });
    }
  };

  const inputClass = "w-full bg-[#2a2d38] border border-[#4E5564] rounded-lg px-4 py-2.5 text-white placeholder-gray-500 focus:outline-none focus:border-[#B5A593] transition-colors";
  const errorClass = "border-red-500 focus:border-red-500";
  const labelClass = "block text-sm font-medium text-gray-300 mb-2";
  const errorTextClass = "text-red-400 text-xs mt-1";

  return (
    <div className="space-y-4 p-6 bg-[#1A1D29] border border-[#4E5564] rounded-xl">
      {label && <h3 className="text-lg font-semibold text-[#B5A593] mb-4">{label}</h3>}
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className={labelClass}>Date of Birth</label>
          <input
            type="date"
            value={data.date}
            onChange={handleChange('date')}
            className={`${inputClass} ${errors.date ? errorClass : ''}`}
          />
          {errors.date && <p className={errorTextClass}>{errors.date}</p>}
        </div>

        <div>
          <label className={labelClass}>Time of Birth</label>
          <input
            type="time"
            value={data.time}
            onChange={handleChange('time')}
            disabled={unknownTime}
            className={`${inputClass} ${errors.time ? errorClass : ''} ${unknownTime ? 'opacity-60 cursor-not-allowed text-transparent' : ''}`}
          />
          <label className="flex items-center mt-2 text-sm text-gray-400 cursor-pointer">
            <input
              type="checkbox"
              checked={unknownTime}
              onChange={handleUnknownTimeChange}
              className="mr-2 w-4 h-4 accent-[#B5A593]"
            />
            I don't know my birth time
          </label>
          {errors.time && <p className={errorTextClass}>{errors.time}</p>}
        </div>
      </div>

      <div>
        <label className={labelClass}>Birth Location</label>
        <LocationSearch
          onSelect={(lat, lon, name) => {
            onChange({ 
              ...data, 
              latitude: lat.toString(), 
              longitude: lon.toString() 
            });
          }}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className={labelClass}>Latitude</label>
          <input
            type="text"
            value={data.latitude}
            placeholder="Auto-filled from location search"
            className={`${inputClass} opacity-60 cursor-not-allowed`}
            readOnly
          />
        </div>

        <div>
          <label className={labelClass}>Longitude</label>
          <input
            type="text"
            value={data.longitude}
            placeholder="Auto-filled from location search"
            className={`${inputClass} opacity-60 cursor-not-allowed`}
            readOnly
          />
        </div>
      </div>
      {(errors.latitude || errors.longitude) && (
        <p className={errorTextClass}>
          {errors.latitude || errors.longitude}
        </p>
      )}
    </div>
  );
};
