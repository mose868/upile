'use client';

import React, { useState } from 'react';
import Image from 'next/image';
import { FaSearch } from 'react-icons/fa';
import { useRouter } from 'next/navigation'; 
import UpdateCard from '../UpdateCard';
import PersonCard from '../PersonCard';
import { useMissingPersons } from '../hooks/useMissingPersons';

const ITEMS_PER_PAGE = 6;

const PublicDashboard: React.FC = () => {
  const { data, loading, error } = useMissingPersons();
  const [searchTerm, setSearchTerm] = useState('');
  const [activeTab, setActiveTab] = useState<string>('Total Missing Persons');
  const [selectedLocation, setSelectedLocation] = useState<string>('All Locations');
  const [currentPage, setCurrentPage] = useState(1);
  const router = useRouter();

  const uniqueLocations = ['All Locations', ...Array.from(new Set(data?.map((person) => person.location)))];

  const filteredPersons = data?.filter((person) => {
    const matchesSearchTerm = person.first_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      person.last_name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesLocation = selectedLocation === 'All Locations' || person.location === selectedLocation;
    return matchesSearchTerm && matchesLocation;
  }).sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()) || [];

  const updateCategories = [
    { title: 'Total Stats', count: filteredPersons.length },
    { title: 'Missing', count: filteredPersons.filter((p) => p.status === 'missing').length },
    { title: 'Found', count: filteredPersons.filter((p) => p.status === 'found').length },
    { title: 'Departed', count: filteredPersons.filter((p) => p.status === 'departed').length },
  ];

  const filteredByTab = () => {
    switch (activeTab) {
      case 'Missing':
        return filteredPersons.filter((p) => p.status === 'missing');
      case 'Departed':
        return filteredPersons.filter((p) => p.status === 'departed');
      case 'Found':
        return filteredPersons.filter((p) => p.status === 'found');
      default:
        return filteredPersons;
    }
  };

  const totalPages = Math.ceil(filteredByTab().length / ITEMS_PER_PAGE);
  const paginatedPersons = filteredByTab().slice((currentPage - 1) * ITEMS_PER_PAGE, currentPage * ITEMS_PER_PAGE);

  const goToPreviousPage = () => setCurrentPage((prevPage) => Math.max(prevPage - 1, 1));
  const goToNextPage = () => setCurrentPage((prevPage) => Math.min(prevPage + 1, totalPages));

  return (
    <div className="bg-white min-h-screen">
      <header className="bg-[#662113] text-white p-4">
        <div className="container mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <Image
            src='/media/lostlocatelogo.png'
            alt='LostLocate Logo'
            className='w-24 sm:w-32 ml-0 sm:ml-0'
            width={500}
            height={300}
            priority
          />
          <h1 className="text-[#D4B337] text-center text-[24px] sm:text-[40px] flex-grow">
            Locating Lost Ones
          </h1>
          <button
            onClick={() => router.push('/login')}
            className="mt-4 sm:mt-0 bg-[#D4B337] hover:bg-[#bba72f] text-[#662113] font-semibold py-2 px-6 rounded-full shadow-lg transition duration-200 ease-in-out transform hover:scale-105"
          >
            Manage Data
          </button>
        </div>
      </header>
      <main className="container mx-auto px-2 sm:px-4 md:px-8 py-4">
        <section className="flex flex-col sm:flex-row justify-between items-center mt-8 mb-4 gap-4">
          <h2 className="text-[24px] sm:text-[30px] font-bold text-[#662113]">Missing Persons Updates</h2>
          <select
            className="border border-[#662113] px-4 py-2 rounded-md"
            value={selectedLocation}
            onChange={(e) => {
              setSelectedLocation(e.target.value);
              setCurrentPage(1);
            }}
          >
            {uniqueLocations.map((location) => (
              <option key={location} value={location}>
                {location}
              </option>
            ))}
          </select>
        </section>
        <div className="overflow-x-auto">
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 mb-8">
            {updateCategories.map((category) => (
              <UpdateCard
                key={category.title}
                title={category.title}
                count={category.count}
                isActive={category.title === activeTab}
                onClick={() => {
                  setActiveTab(category.title);
                  setCurrentPage(1);
                }}
              />
            ))}
          </div>
        </div>
        <div className="flex flex-col sm:flex-row justify-between items-center mb-4 gap-4">
          <h2 className="text-[24px] sm:text-[30px] font-bold text-[#662113] mb-4 sm:mb-0">Recent Cases</h2>
          <div className="relative w-full sm:w-96">
            <input
              type="text"
              placeholder="Search..."
              className="border border-[#662113] rounded-full px-4 py-2 w-full pl-10"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            <FaSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-[#662113]" />
          </div>
        </div>

          {loading ? (
            <p>Loading...</p>
          ) : error ? (
            <p>{error.message}</p>
          ) : paginatedPersons.length === 0 ? (
            <p>Not Found.</p>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {paginatedPersons.map((person, index) => (
                <PersonCard
                  key={index}
                  first_name={person.first_name}
                  last_name={person.last_name}
                  age={person.age}
                  gender={person.gender}
                  location={person.location}
                  image={person.image}
                  clothes_worn={person.clothes_worn}
                  missing_date={person.missing_date}
                  status= { person.status}
                  id={''} contact={''} height={0} weight={0} hair_color={''} eye_color={''} skin_color={''} created_at={person.created_at} officer_id={0}
                />
              ))}
            </div>
          )}

          <div className="flex justify-center items-center mt-4">
            <button
              onClick={goToPreviousPage}
              disabled={currentPage === 1}
              className={`px-4 py-2 mx-2 ${currentPage === 1 ? 'text-gray-400' : 'text-[#662113] hover:bg-[#D4B337]'} font-bold`}
            >
              Previous
            </button>
            <span className="text-[#662113] font-bold">
              Page {currentPage} of {totalPages}
            </span>
            <button
              onClick={goToNextPage}
              disabled={currentPage === totalPages}
              className={`px-4 py-2 mx-2 ${currentPage === totalPages ? 'text-gray-400' : 'text-[#662113] hover:bg-[#D4B337]'} font-bold`}
            >
              Next
            </button>
          </div>
      </main>
    </div>
  );
};

export default PublicDashboard;
