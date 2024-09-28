import React from "react";
import { useNavigate } from "react-router-dom";

export default function PersonaForm() {
  const navigate = useNavigate();
  return (
    <div className="flex flex-col items-center gap-5">
      <div className="grid grid-cols-2 gap-5 mt-5">
        <label className="block text-formLabelText font-bold mb-1 md:mb-0 pr-4">
          Name
        </label>
        <input
          type="text"
          className="bg-inputBackground appearance-none border-2 border-inputBorder rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:border-inputFocus"
        />
        <label className="block text-formLabelText font-bold  mb-1 md:mb-0 pr-4">
          Description
        </label>
        <textarea className="bg-inputBackground appearance-none border-2 border-inputBorder rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:border-inputFocus" />
        <label className="block text-formLabelText font-bold mb-1 md:mb-0 pr-4">
          Avatar
        </label>
        <input type="file" name="avatar" accept="image/png, image/jpeg" />
        <label className="block text-formLabelText font-bold mb-1 md:mb-0 pr-4">
          Documents
        </label>
        <input type="file" name="documents" accept="text/plain" />
      </div>
      <button
        className="bg-primaryButton text-primaryButtonText rounded-full py-1 px-5 font-semibold w-32"
        onClick={() => {
          navigate("/");
        }}
      >
        Submit
      </button>
      <button
        className="bg-secondaryButton text-secondaryButtonText rounded-full py-1 px-5 font-semibold w-32"
        onClick={() => {
          navigate("/");
        }}
      >
        Exit
      </button>
    </div>
  );
}
