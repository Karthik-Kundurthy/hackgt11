import React from "react";
import { useNavigate } from "react-router-dom";

interface PersonaFormProps {
  personaFormHandler: (
    name: string,
    description: string,
    avatar: any,
    documents: any,
  ) => Promise<void>;
  name?: string;
  description?: string;
  avatar?: any;
  isEdit?: boolean;
}
export default function PersonaForm(props: PersonaFormProps) {
  const navigate = useNavigate();
  const {
    personaFormHandler,
    name: nameProp,
    description: descriptionProp,
    isEdit: isEditProp,
  } = props;
  const [name, setName] = React.useState(nameProp ?? "");
  const [description, setDescription] = React.useState(descriptionProp ?? "");
  const [avatar, setAvatar] = React.useState<any>(null);
  const [files, setDocuments] = React.useState<any>(null);

  return (
    <div className="flex flex-col items-center gap-5">
      <div className="grid grid-cols-2 gap-5 mt-5">
        <label className="block text-formLabelText font-bold mb-1 md:mb-0 pr-4">
          Name
        </label>
        {isEditProp ? (
          <span className="appearance-none w-full py-2 px-4 text-gray-700 leading-tight">
            {name}
          </span>
        ) : (
          <input
            type="text"
            value={name}
            className="bg-inputBackground appearance-none border-2 border-inputBorder rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:border-inputFocus"
            onChange={(e) => setName(e.target.value)}
          />
        )}
        <label className="block text-formLabelText font-bold  mb-1 md:mb-0 pr-4">
          Description
        </label>
        <textarea
          className="bg-inputBackground appearance-none border-2 border-inputBorder rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:border-inputFocus"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <label className="block text-formLabelText font-bold mb-1 md:mb-0 pr-4">
          Avatar
        </label>
        <input
          type="file"
          name="avatar"
          accept="image/png, image/jpeg"
          className="block w-full bg-inputBackground appearance-none border-2 border-inputBorder rounded py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:border-inputFocus"
          onChange={(e) => setAvatar(e.target.files![0])}
        />
        <label
          className="block text-formLabelText font-bold mb-1 md:mb-0 pr-4"
          htmlFor="multiple_files"
        >
          Documents
        </label>
        <input
          className="block w-full bg-inputBackground appearance-none border-2 border-inputBorder rounded py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:border-inputFocus"
          id="multiple_files"
          type="file"
          accept="text/plain"
          onChange={(e) => setDocuments(e.target.files)}
          multiple
        />
      </div>
      <button
        className="bg-primaryButton text-primaryButtonText rounded-full py-1 px-5 font-semibold w-32"
        onClick={async () => {
          await personaFormHandler(name, description, avatar, files);
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
