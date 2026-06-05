import { Link } from 'react-router-dom';
import { FaHome } from 'react-icons/fa';

interface Crumb {
  label: string;
  path?: string;
}

interface BreadcrumbsProps {
  crumbs: Crumb[];
}

const Breadcrumbs = ({ crumbs }: BreadcrumbsProps) => {
  return (
    <ul className="breadcrumbs">
      <li>
        <Link to="/">
          <FaHome size={18} />
        </Link>
      </li>
      {crumbs.map((crumb, idx) => (
        <li key={idx} className={idx === crumbs.length - 1 ? 'active' : ''}>
          <span className="separator">/</span>
          {crumb.path && idx !== crumbs.length - 1 ? (
            <Link to={crumb.path}>{crumb.label}</Link>
          ) : (
            <span>{crumb.label}</span>
          )}
        </li>
      ))}
    </ul>
  );
};

export default Breadcrumbs;