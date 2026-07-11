import './Header.css';

export default function Header() {
  return (
    <header className="header">
      <h1 className="header__title">Autonomous Data Cleansing Engine</h1>
      <p className="header__subtitle">
        Upload your uncleaned CSV file to clean and optimize it.
      </p>
    </header>
  );
}
