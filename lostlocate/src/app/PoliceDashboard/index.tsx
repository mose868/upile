'use client';
import React from 'react';
import ChartComponent from '../Chart/policeChart';
import { useMissingPersons } from '../hooks/useMissingPersons';


const PoliceDashboard = () => {
  const { data, loading, error } = useMissingPersons();

  if (loading) {
    return <p>Loading ...</p>;
  }

  if (error) {
    return <p>Error: {error.message}</p>;
  }

  
  const successfulMatches = data.filter(person => person.status === 'found').length;
  const openCases = data.filter(person=> person.status === 'missing').length;
  const closedCases = data.filter(person=> person.status === 'departed').length + data.filter(person => person.status === 'found').length;

  return (
    <div className="min-h-screen w-full flex flex-col bg-gray-100 px-2 sm:px-4 md:px-8 py-4">
      <div className="container mx-auto">
        <div className="flex flex-col md:flex-row flex-wrap gap-4 md:gap-8 mt-6 justify-center items-stretch">
          <div className="bg-[#D4B337] text-white text-center text-lg sm:text-xl md:text-2xl font-bold p-4 sm:p-6 rounded-lg shadow-md w-full max-w-xs flex-1">
            Successful Matches:<br/> <span className="text-2xl sm:text-3xl md:text-4xl">{successfulMatches}</span>
          </div>
          <div className="bg-[#662113] text-white text-center text-lg sm:text-xl md:text-2xl font-bold p-4 sm:p-6 rounded-lg shadow-md w-full max-w-xs flex-1">
            Open Cases:<br/> <span className="text-2xl sm:text-3xl md:text-4xl">{openCases}</span>
          </div>
          <div className="bg-[#8D4004] text-white text-center text-lg sm:text-xl md:text-2xl font-bold p-4 sm:p-6 rounded-lg shadow-md w-full max-w-xs flex-1">
            Closed Cases: <br/><span className="text-2xl sm:text-3xl md:text-4xl">{closedCases}</span>
          </div>
        </div>
        <div className="mt-8 flex flex-col items-center">
          <div className="w-full max-w-3xl">
            <ChartComponent />
          </div>
        </div>
      </div>
    </div>
  );
};

export default PoliceDashboard;