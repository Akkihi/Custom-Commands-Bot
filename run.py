from auth import dp, runner
import handlers

if __name__ == '__main__':
    runner.start_polling(dp)
