import { IoIosAdd } from "react-icons/io";
import { useNavigate } from "react-router-dom";

export default function AddPersonaCard() {
  // create a new persona
  const navigate = useNavigate();

  return (
    <div className="flex border-2 rounded-xl border-secondaryButton border-dashed p-3 w-full h-32">
      <button
        className="flex items-center justify-center w-full"
        onClick={() => {
          navigate("/create");
        }}
      >
        <IoIosAdd className="w-10 h-10" />
        <p className="text-md text-secondaryButtonText">Add Persona</p>
      </button>
    </div>
  );
}
