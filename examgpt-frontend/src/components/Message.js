import React from 'react';

const Message = props => {
  const { message, fontClass } = props

  return (
    <div className="row justify-content-center mt-5">
      {
        message.length === 0 ?
          <div>
            <span>&nbsp;&nbsp;</span>
          </div> :
          <div className={fontClass}>
            {message}
          </div>
      }
    </div>
  );
}

export default Message;
