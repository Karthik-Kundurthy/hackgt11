import { IoIosAdd } from "react-icons/io";

export default function AddPersonaCard() {
  // create a new persona

  return (
    <div className="flex border-2 rounded-xl border-secondaryButton border-dashed p-3 w-full h-32">
      <button className="flex items-center justify-center w-full">
        <IoIosAdd className="w-10 h-10" />
        <p className="text-md text-secondaryButtonText">Add Persona</p>
      </button>
    </div>
  );
}
