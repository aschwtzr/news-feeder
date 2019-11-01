import React from 'react';
// import './css/NavBar.css';

function TabBar() {
  return (
    <div classNameName="">
      <div class="tabs is-boxed">
        <ul>
          <li class="is-active">
            <a>
              <span class="icon is-small"><i class="fas fa-image" aria-hidden="true"></i></span>
              <span>Feeds</span>
            </a>
          </li>
          <li>
            <a>
              <span class="icon is-small"><i class="fas fa-music" aria-hidden="true"></i></span>
              <span>Google</span>
            </a>
          </li>
          <li>
            <a>
              <span class="icon is-small"><i class="fas fa-film" aria-hidden="true"></i></span>
              <span>Briefings</span>
            </a>
          </li>
          <li>
            <a>
              <span class="icon is-small"><i class="far fa-file-alt" aria-hidden="true"></i></span>
              <span>Settings</span>
            </a>
          </li>
        </ul>
      </div>
    </div>
  );
}

export default TabBar;