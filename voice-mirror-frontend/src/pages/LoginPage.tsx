import Title from "../components/Title";
import { Navigate } from "react-router-dom";
import { useState, useContext } from "react";
import { ProfileContext } from "../contexts/ProfileContext";

export default function LoginPage() {
  const [error, setError] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const { profile, handleLogin } = useContext(ProfileContext);

  const onSubmit = async (e: any) => {
      e.preventDefault();
      if (password === "") {
        setError(true);
      } else {
        await handleLogin(username, password);
      }
  };
    
  if (profile) {
    return <Navigate to="/" />;
  }


  return (
    <div className="w-full h-full flex items-center justify-center">
      <div className="w-full max-w-sm">
        <Title />
        <form className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4" onSubmit={onSubmit}>
          <div className="mb-4">
            <label
              className="block text-formLabelText text-sm font-bold mb-2"
              htmlFor="username"
            >
              Username
            </label>
            <input
              className="shadow appearance-none border rounded w-full py-2 px-3 text-formLabelText leading-tight focus:outline-none focus:shadow-outline"
              id="username"
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          <div className="mb-6">
            <label
              className="block text-formLabelText text-sm font-bold mb-2"
              htmlFor="password"
            >
              Password
            </label>
            <input
              className={`shadow appearance-none border ${error ? "border-error" : ""} rounded w-full py-2 px-3 text-formLabelText mb-3 leading-tight focus:outline-none focus:shadow-outline`}
              id="password"
              type="password"
              placeholder="******************"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            {error && (
              <p className="text-error text-xs italic">
                Please choose a password.
              </p>
            )}
          </div>
          <div className="flex items-center justify-between">
            <button
              className="bg-primaryButton hover:bg-primaryButtonHover text-primaryButtonText font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full"
              type="submit"
            >
              Sign In
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
